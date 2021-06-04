import React from "react";

// Material UI
import { DataGrid } from "@material-ui/data-grid";

const columns = [
  { field: "score", headerName: "Score", width: 120 },
  { field: "title", headerName: "Title", width: 400 },
];

var rows = [];

const DataDisplay = (props) => {
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
};

export default DataDisplay;
