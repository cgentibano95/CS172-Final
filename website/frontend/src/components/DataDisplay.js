import React from "react";

// Material UI
import { DataGrid } from "@material-ui/data-grid";

const columns = [
  { field: "title", headerName: "Title", width: 150 },
  { field: "score", headerName: "Score", width: 150 },
];

var rows = [];

const DataDisplay = (props) => {
  if (props.data === undefined) {
    return (
      <div>
        <p> no results! </p>
      </div>
    );
  } else {
    return (
      <div style={{ height: 500, widht: "100%" }}>
        <DataGrid
          rows={props.data}
          columns={columns}
          pageSize={7}
          className={props.dataGrid}
        />
      </div>
    );
  }
};

export default DataDisplay;
