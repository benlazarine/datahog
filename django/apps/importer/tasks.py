from irods.session import iRODSSession
from irods.models import DataObject, Collection
from irods.column import Between

from celery import shared_task
from django.db import transaction

from .models import ImportAttempt
from apps.file_data.models import File, Folder, FileType, FileSummary

@shared_task
def import_files_from_irods(attempt_id, password):
    attempt = ImportAttempt.objects.get(id=attempt_id)

    total_size = 0
    file_count = 0
    folder_count = 0

    file_objects = []
    folder_objects_by_path = {}
    file_types_by_extension = {}

    try:
        attempt.current_step = 1
        attempt.save()
        print('Requesting data from iRODS...')
        with iRODSSession(
            user=attempt.irods_user,
            password=password,
            host=attempt.irods_host,
            port=attempt.irods_port,
            zone=attempt.irods_zone
        ) as session:
            query = session.query(
                Collection.name,
                DataObject.name,
                DataObject.checksum,
                DataObject.size,
                DataObject.create_time
            ).filter(
                DataObject.replica_number == 0
            ).filter(
                Between(Collection.name, (
                    attempt.top_folder, 
                    attempt.top_folder + '~'
                ))
            ).limit(1000)

            for result_set in query.get_batches():
                if attempt.current_step != 2:
                    attempt.current_step = 2
                    attempt.save()
                    print('Receiving data batches...')
                for row in result_set:
                    file_path = '{}/{}'.format(row[Collection.name], row[DataObject.name])

                    file_objects.append(File(
                        name=row[DataObject.name],
                        path=file_path,
                        size=row[DataObject.size],
                        date_created=row[DataObject.create_time],
                        checksum=row[DataObject.checksum]
                    ))

        attempt.current_step = 3
        attempt.save()
        print('Creating objects...')
        for file_obj in file_objects:

            file_count += 1
            total_size += file_obj.size

            # find parent folder's path
            last_slash = file_obj.path.rfind('/')
            parent_path = file_obj.path[:last_slash]
            child_obj = file_obj

            # update all parent folders
            while len(parent_path) > 0:
                last_slash = parent_path.rfind('/')
                if parent_path in folder_objects_by_path:
                    parent_obj = folder_objects_by_path[parent_path]
                    parent_obj.total_size += file_obj.size
                else:
                    # if the parent folder doesn't exist yet, create it
                    parent_obj = Folder(
                        path=parent_path,
                        name=parent_path[last_slash+1:],
                        total_size=file_obj.size
                    )
                    folder_objects_by_path[parent_path] = parent_obj
                    folder_count += 1

                # iterate up the hierarchy
                child_obj.parent = parent_obj
                if parent_path == attempt.top_folder:
                    break
                child_obj = parent_obj
                parent_path = parent_path[:last_slash]

            # find file type
            last_dot = file_obj.name.rfind('.')
            if last_dot != -1:
                extension = file_obj.name[last_dot+1:]
                if extension in file_types_by_extension:
                    file_type = file_types_by_extension[extension]
                    file_type.total_size += file_obj.size
                else:
                    # if this file type doesn't exist yet, create it
                    file_type = FileType(
                        name=extension,
                        extension_pattern=extension,
                        total_size=file_obj.size
                    )
                    file_types_by_extension[extension] = file_type

                file_obj.file_type = file_type

        if attempt.top_folder in folder_objects_by_path:
            folder_objects_by_path[attempt.top_folder].name = attempt.top_folder

        attempt.current_step = 4
        attempt.save()
        print('Filling database...')
        with transaction.atomic(using='file_data'):
            FileType.objects.all().delete()
            File.objects.all().delete()
            Folder.objects.all().delete()

            File.objects.bulk_create(file_objects)
            Folder.objects.bulk_create(folder_objects_by_path.values())
            FileType.objects.bulk_create(file_types_by_extension.values())
            FileSummary.objects.create(
                folder_count=folder_count,
                file_count=file_count,
                total_size=total_size
            )

            attempt.in_progress = False
            attempt.failed = False
            attempt.save()

        print('Database update successful.')
            
    except Exception as e:
        print('Database update failed due to error: {}'.format(e))
        attempt.in_progress = False
        attempt.failed = True
        attempt.save()
