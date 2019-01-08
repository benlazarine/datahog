import React from 'react';
import { FileTable } from './fileTable';
import { PaginatedPanel } from './paginatedPanel';
import { LoadingBox } from './loadingBox';
import { Link } from 'react-router-dom';
import { SizeTimeline } from './sizeTimeline';

export class SummaryTab extends React.Component {

    constructor(props) {
        super(props);
        
        this.state = {
            summary: {}
        };

        this.onLoad = this.onLoad.bind(this);
    }

    onLoad(response) {
        this.setState({
            summary: response.data
        });
    }

    render() {
        return (
            <LoadingBox get="/api/files/summary" callback={this.onLoad} checkForUpdate={true}>
                <div className="container">
                    <div className="columns">
                        <div className="column">
                            <div className="card fixed-height">
                                <div className="card-header">
                                    <div className="card-title h5">You have...</div>
                                </div>
                                <div className="card-body">
                                    <p>
                                        <i className="fa fa-fw fa-file"></i>
                                        {this.state.summary.file_count} files
                                    </p>
                                    <p>
                                        <i className="fa fa-fw fa-folder-open"></i>
                                        {this.state.summary.folder_count} folders
                                    </p>
                                    <p>
                                        {this.state.summary.duplicate_count > 0 ? 
                                            <Link to="/duplicates">
                                                <i className="fa fa-fw fa-clone"></i>
                                                {this.state.summary.duplicate_count} duplicate files
                                            </Link> :
                                            <React.Fragment>
                                                <i className="fa fa-fw fa-clone"></i>
                                                0 duplicate files
                                            </React.Fragment>
                                        }
                                    </p>
                                </div>

                                <div className="visualization">
                                    <SizeTimeline data={this.state.summary.size_timeline_data} id="sizeTimeline"/>
                                </div>
                                <div className="card-footer">
                                    Last updated {this.state.summary.timestamp}
                                </div>
                            </div>
                        </div>
                        <div className="column">
                            <PaginatedPanel 
                                scroll={false}
                                title="Top File Types"
                                get="/api/files/biggestfiletypes"
                                component={FileTable}/>
                        </div>
                    </div>
                    <div className="columns">
                        <div className="column">
                            <PaginatedPanel
                                scroll={false}
                                title="Biggest Files"
                                get="/api/files/biggestfiles"
                                component={FileTable}/>
                        </div>
                        <div className="column">
                            <PaginatedPanel
                                scroll={false}
                                title="Biggest Folders"
                                get="/api/files/biggestfolders"
                                component={FileTable}/>
                        </div>
                    </div>
                </div>
            </LoadingBox>
        );
    }
}