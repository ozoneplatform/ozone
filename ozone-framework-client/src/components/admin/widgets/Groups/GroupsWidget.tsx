import * as React from "react";

import { Button, ButtonGroup, Divider, Intent } from "@blueprintjs/core";
import { AdminTable } from "../../table/AdminTable";

import { GroupCreateForm } from "./GroupCreateForm";

import { lazyInject } from "../../../../inject";

import { GroupAPI, GroupCreateRequest, GroupDTO } from "../../../../api";


interface State {
    groups: GroupDTO[];
    loading: boolean;
    pageSize: number;
    columns: any;
    showTable: boolean;
    showCreate: boolean;
}

// TODO
// Modify widget to take in widget values from administration menu and launch from menu
// Pagination handling with client API
// Style
// Popup warning dialogue for deleting
// Error handling for form

export class GroupsWidget extends React.Component<{}, State> {

    @lazyInject(GroupAPI)
    private groupAPI: GroupAPI;

    constructor(props: any) {
        super(props);
        this.state = {
            groups: [],
            loading: true,
            pageSize: 5,
            showTable: true,
            showCreate: false,
            columns: [
                {
                    Header: "Groups",
                    columns: [
                        {
                            Header: "Group Name",
                            accessor: "name",
                            Footer: (
                                // TODO - Keep in footer or move to below table
                                <Button
                                    text="Create"
                                    intent={Intent.SUCCESS}
                                    icon="add"
                                    small={true}
                                    onClick={() => this.toggleCreate()}
                                    data-element-id='group-admin-widget-create-button'
                                />
                            )
                        },
                        {
                            Header: "Users",
                            accessor: "totalUsers"
                        },
                        {
                            Header: "Widgets",
                            accessor: "totalWidgets"
                        },
                        {
                            // TODO - Access totalDashboards (Apps) in old OWF
                            Header: "Dashboards",
                            accessor: "totalDashboards"
                        }
                    ],

                },
                // TODO - Abstract this to only have to provide onclick function name with styled buttons
                {
                    Header: "Actions",
                    Cell: (row: any) => (
                        <div>
                            <ButtonGroup>
                                <Button
                                    text="Edit"
                                    intent={Intent.PRIMARY}
                                    icon="edit"
                                    small={true}
                                    onClick={() => this.getGroupById(row.original.id)}
                                />
                                <Divider/>
                                <Button
                                    text="Delete"
                                    intent={Intent.DANGER}
                                    icon="trash"
                                    disabled={true}
                                    small={true}
                                    // onClick={() => this.deleteUserById(row.original.id)}
                                />
                            </ButtonGroup>
                        </div>
                    )
                }
            ]
        };
    }

    componentDidMount() {
        this.getGroups();
    }

    render() {
        const showTable = this.state.showTable;
        const showCreate = this.state.showCreate;

        return (
            <div data-element-id="group-admin-widget-dialog">
                {showTable &&
                <AdminTable
                    data={this.state.groups}
                    columns={this.state.columns}
                    loading={this.state.loading}
                    pageSize={this.state.pageSize}
                />
                }
                {showCreate &&
                  <GroupCreateForm onSubmit={this.createGroup}
                                  onCancel={this.toggleCreate}/>
                }
            </div>
        );
    }

    private toggleCreate = () => {
        this.setState({
            showCreate: !this.state.showCreate,
            showTable: !this.state.showTable
        });
    }

    private getGroups = async () => {
        const response = await this.groupAPI.getGroups();

        // TODO: Handle failed request
        if (response.status !== 200) return;

        this.setState({
            groups: response.data.data,
            loading: false
        });
    }

    private getGroupById = async (id: number) => {
        const response = await this.groupAPI.getGroupById(id);

        // TODO: Handle failed request
        if (response.status !== 200) return;
    }

    private createGroup = async (data: GroupCreateRequest) => {
        console.log(data);
        const response = await this.groupAPI.createGroup(data);

        // TODO: Handle failed request
        if (response.status !== 200) return false;

        this.toggleCreate();
        this.setState({ loading: true });
        this.getGroups();

        return true;
    }

}
