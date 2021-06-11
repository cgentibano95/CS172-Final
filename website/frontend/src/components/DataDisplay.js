import React from "react";

// Material UI
import { DataGrid } from "@material-ui/data-grid";

const columns = [
  { field: "score", headerName: "Score", width: 120 },
  { field: "title", headerName: "Title", width: 400 },
  { field: "url", headerName: "URL", width: 400 },
  { field: "text", headerName: "Text", width: 600 },
];

const DataDisplay = (props) => {
  return (
    <div style={{ height: 500, widht: "100%" }}>
      <DataGrid
        rows={props.data}
        columns={columns}
        pageSize={10}
        className={props.dataGrid}
      />
    </div>
  );
};

export default DataDisplay;
