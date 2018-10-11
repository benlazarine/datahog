import React from 'react';
import { Size, ClickToCopy } from './util';

export class SimpleFileTable extends React.Component {
    render() {
        return (
            <table>
                <thead>
                    <tr>
                        <th>{this.props.title}</th>
                    </tr>
                </thead>
                <tbody>
                    {this.props.files.map(file => {
                        return <SimpleFileTableRow 
                                file={file} 
                                key={file.id} 
                                onRowClick={this.props.onRowClick} 
                                selectedRow={this.props.selectedRow}/>
                    })}
                </tbody>
            </table>
        );
    }
}

export class SimpleFileTableRow extends React.Component {
    constructor(props) {
        super(props);
        this.handleRowClick = this.handleRowClick.bind(this);
    }
    handleRowClick() {
        this.props.onRowClick(this);
    }
    render() {
        return (
            <tr>
                <td>
                    {this.props.file.name}
                    {this.props.file.path && <ClickToCopy text={this.props.file.path} />}
                </td>
                <td>
                    <Size bytes={this.props.file.size || this.props.file.total_size}/>
                </td>
            </tr>
        )
    }
}

