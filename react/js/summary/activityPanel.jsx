import React from 'react';
import axios from '../axios';
import { ActivityTimeline } from './activityTimeline';

/**
 * A panel describing file creation/modification/access in the recent past.
 */
export class ActivityPanel extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            loading: true,
            error: false,
            created: 0,
            show_created: true,
            modified: 0,
            show_modified: true,
            accessed: 0,
            show_accessed: true,
            total: 0,
            graph_data: [],
            days: 30
        };
        
        this.onLoad = this.onLoad.bind(this);
        this.onError = this.onError.bind(this);
        this.onChange = this.onChange.bind(this);

        this.cancelToken = axios.CancelToken.source();
        axios.get('/api/filedata/activity', {
            params: {
                source: this.props.source,
                days: this.state.days
            },
            cancelToken: this.cancelToken.token
        })
        .then(this.onLoad)
        .catch(this.onError);
    }

    onLoad(response) {
        this.setState({
            created: response.data.modified,
            modified: response.data.modified,
            accessed: response.data.accessed,
            graph_data: response.data.graph_data,
            total: response.data.total,
            loading: false,
            error: false
        });
    }
    
    onError(error) {
        this.setState({
            loading: false,
            error: true
        });
    }

    componentWillUnmount() {
        if (this.cancelToken) this.cancelToken.cancel();
    }

    onChange(event) {
        this.setState({
            days: event.target.value,
            loading: true
        });
    }

    render() {
        return (
            <div className="card fixed-height">
                <div className="card-header">
                    <div className="card-title h5">File Activity from the last</div>
                </div>
                <div className="card-body columns">
                    <div className="column">
                        <select value={this.state.days} className="form-select" onChange={this.onChange}>
                            <option value={7}>7 days</option>
                            <option value={30}>30 days</option>
                            <option value={90}>90 days</option>
                        </select>
                        Created: {this.state.created},
                        Modified: {this.state.modified},
                        Accessed: {this.state.accessed}
                    </div>
                    <div className="column">
                        <ActivityTimeline 
                            data={this.state.graph_data}
                            days={this.state.days}
                            id="activityTimeline"
                        />
                    </div>
                </div>
            </div>
        );
    }
}