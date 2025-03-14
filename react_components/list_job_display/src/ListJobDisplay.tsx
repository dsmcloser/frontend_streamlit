import { BaseProvider, DarkTheme } from 'baseui';

import React, { createRef } from 'react';
import { List, ListItem, ListItemButton, Box, Card, CardContent, Typography, ListItemIcon } from '@mui/material';

import { Timeline, TimelineItem, TimelineSeparator, TimelineConnector, TimelineContent, TimelineDot, TimelineOppositeContent } from '@mui/lab';
import AccessTimeIcon from '@mui/icons-material/AccessTime';

import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { darcula } from 'react-syntax-highlighter/dist/esm/styles/prism';

import { Client as Styletron } from 'styletron-engine-atomic'
import { Provider as StyletronProvider } from 'styletron-react'
import {
    ComponentProps,
    withStreamlitConnection,
    StreamlitComponentBase,
} from 'streamlit-component-lib'


// Initialize our Styletron engine
const engine = new Styletron()


interface State {
    selectedItem: number | null;
}


class ListJobDisplay extends StreamlitComponentBase<State> {
    private readonly detailedInfo: Array<any>;
    private readonly jobDisplayRef: React.RefObject<HTMLDivElement>;

    constructor(props: ComponentProps) {
        super(props);
        this.detailedInfo = this.props.args["items_information"];
        this.renderRow = this.renderRow.bind(this);
        this.state = {
            selectedItem: this.props.args["selected_id"],
        };
        this.jobDisplayRef = createRef();

    }

    handleClick = (index: number) => {
        this.setState({ selectedItem: index });
        if (this.jobDisplayRef.current) {
            this.jobDisplayRef.current.scrollTop = 0;
        }
    }

    public renderRow(index: number) {
        return (
            <ListItem key={index} component="div" disablePadding>
                <ListItemButton onClick={() => this.handleClick(index)} className="list-item-button">
                    <div>
                        {this.detailedInfo[index]["file_name"]}
                    </div>
                    <div className="hidden-text">
                        <p style={{ marginTop: 2, marginBottom: 2 }}>
                            <b>ID: </b>{this.detailedInfo[index]["id"]}
                        </p>
                        <p style={{ marginTop: 2, marginBottom: 2 }}>
                            <AccessTimeIcon />
                            {" " + this.detailedInfo[index]["date_updated"].slice(0, 19)}
                        </p>
                    </div>
                </ListItemButton>
            </ListItem>
        );
    }

    public renderIssue(prompt_info: any) {
        const issues_element = [];
        if (!((prompt_info["validation_status"] === "Warning") || (prompt_info["validation_status"] === "Not validated"))) return []
        for (const issue of prompt_info["issues"]) {
            issues_element.push(
                <List>
                    <ListItem>
                        <div>
                            <b>Line: </b>{issue["line"]}
                        </div>
                    </ListItem>
                    <ListItem>
                        <div>
                            <b>Section: </b>{issue["section"]}
                        </div>
                    </ListItem>
                    <ListItem>
                        <div>
                            <b>Problem:</b><br></br>
                            {issue["problem"]}
                        </div>
                    </ListItem>
                    <ListItem>
                        <div>
                            <b>Suggestion:</b><br></br>
                            {issue["suggestion"]}
                        </div>
                    </ListItem>
                    <div style={{ borderTop: '1px solid #ccc', margin: '10px 0' }}></div>
                </List>
            );
        }
        return (issues_element)
    }

    public renderTests(content_json: Array<string>) {
        const rows = [];

        if (!content_json.length) return

        for (const prompt_info_json of content_json) {
            const prompt_info = JSON.parse(prompt_info_json);
            let dot_color = "#6c757d";
            let line_color = "#6c757d"
            switch (prompt_info["validation_status"]) {
                case "Not validated":
                    dot_color = "#dc3545";
                    line_color = "#dc3545";
                    break;
                case "Validated":
                    dot_color = "#28a745";
                    line_color = "#28a745";
                    break;
                case "Warning":
                    dot_color = "#ffc107";
                    line_color = "#ffc107";
                    break;
                default:
                    break;
            }
            rows.push(
                <TimelineItem>
                    <TimelineOppositeContent color="textSecondary" width={"48%"}>
                        <div>
                            <h5>
                                <b>Name: </b>{prompt_info["Test"]}
                            </h5>
                        </div>
                        <div>
                            <h5>
                                <b>Status: </b>{prompt_info["validation_status"]}
                            </h5>
                        </div>
                    </TimelineOppositeContent>
                    <TimelineSeparator
                    >
                        <TimelineDot
                            sx={{ backgroundColor: dot_color }}
                        />
                        <TimelineConnector
                            sx={{ backgroundColor: line_color }}
                        />
                    </TimelineSeparator>
                    <TimelineContent width={"48%"}>
                        {this.renderIssue(prompt_info)}
                    </TimelineContent>
                </TimelineItem >
            );
        }
        return (
            <Timeline
                sx={{
                    overflow: "scroll"
                }}
            >
                {rows}
                <div style={{ textAlign: "center" }}>
                    Refresh the page in case some of the choosen tests are not appearing
                </div>
            </Timeline>
        );
    }


    public renderSelectedItem() {
        const { selectedItem } = this.state;

        if (selectedItem === null) return

        console.log(this.detailedInfo[selectedItem]["content_json"])
        console.log(this.detailedInfo[selectedItem]["content_json"] === "")

        let content_info = (this.detailedInfo[selectedItem]["content_json"] !== "" ?
            (<div>
                {this.renderTests(JSON.parse(this.detailedInfo[selectedItem]["content_json"]))}
            </div>) : (<div style={{ textAlign: "center" }}>The tests are still being done. Refresh the page in some seconds</div>))



        return (
            <Card sx={{ padding: 2, bgcolor: 'background.default' }}>
                <CardContent>
                    <div>
                        <h3>
                            Name: {this.detailedInfo[selectedItem]["file_name"]}
                        </h3>
                    </div>
                    <div style={{ borderTop: '1px solid #ccc', margin: '10px 0' }}></div>
                    <div>
                        <b>ID: </b>
                        {this.detailedInfo[selectedItem]["id"]}
                    </div>
                    <p></p>
                    <div>
                        <ListItem style={{ paddingLeft: 0 }}>
                            <ListItemIcon style={{ minWidth: '30px' }}>
                                <AccessTimeIcon />
                            </ListItemIcon>
                            <b>Date created: </b>{this.detailedInfo[selectedItem]["date_created"].slice(0, 19)}
                        </ListItem>
                    </div>
                    <div>
                        <ListItem style={{ paddingLeft: 0 }}>
                            <ListItemIcon style={{ minWidth: '30px' }}>
                                <AccessTimeIcon />
                            </ListItemIcon>
                            <b>Date modified: </b> {this.detailedInfo[selectedItem]["date_updated"].slice(0, 19)}
                        </ListItem>
                    </div>
                    <div style={{ borderTop: '1px solid #ccc', margin: '10px 0' }}></div>
                    <p></p>
                    <div style={{
                        display: 'flex', justifyContent: 'space-between',
                        gap: '16px',
                        backgroundColor: '#2B2B2B',
                        padding: '16px',
                        borderRadius: '8px'

                    }}>
                        <div style={{ width: '48%' }}>
                            <Typography variant="body1" style={{ color: "white" }}>.NET source code:</Typography>
                            <SyntaxHighlighter language="csharp" style={darcula}>
                                {this.detailedInfo[selectedItem]["source_code"]}
                            </SyntaxHighlighter>

                        </div>
                        <div style={{ width: '48%' }}>
                            <Typography variant="body1" style={{ color: "white" }}>Java code migrated:</Typography>

                            <SyntaxHighlighter language="java" style={darcula}>
                                {this.detailedInfo[selectedItem]["code_migrated"]}
                            </SyntaxHighlighter>

                        </div>
                    </div>
                    <div style={{ borderTop: '1px solid #ccc', margin: '10px 0' }}></div>
                    {content_info}
                </CardContent>
            </Card >
        );
    }

    public render = (): React.ReactNode => {
        return (
            <StyletronProvider value={engine}>
                <BaseProvider theme={DarkTheme}>
                    <Box sx={{ display: 'flex', flexDirection: 'row', gap: 0 }}>
                        <Box
                            sx={{ width: '100%', height: '45rem', maxWidth: 250, bgcolor: 'rgb(14, 17, 23)' }}
                        >
                            <List>
                                {this.detailedInfo.map((_, index) => this.renderRow(index))}
                            </List>
                        </Box>
                        <Box
                            sx={{ width: 2, height: '45rem', backgroundColor: 'rgb(14, 17, 23)', }}
                        />
                        <Box
                            sx={{
                                width: '100%', height: '45rem', bgcolor: 'background.paper', overflow: "scroll",
                                backgroundColor: 'rgb(14, 17, 23)',
                                color: 'grey.100'
                            }}
                            ref={this.jobDisplayRef}
                        >
                            {this.renderSelectedItem()}


                        </Box>
                    </Box>
                </BaseProvider>
            </StyletronProvider >
        )
    }
}

export default withStreamlitConnection(ListJobDisplay)
