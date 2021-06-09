import React, { Component } from "react";
import axios from "axios";

// Components
import DataDisplay from "./DataDisplay";

// Material UI
import withStyles from "@material-ui/core/styles/withStyles";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";

const axiosConfig = {
  baseURL: "http://localhost:8080/",
};

const useStyles = (theme) => ({
  textField: {
    margin: "10px auto 10px auto",
    backgroundColor: "white",
  },
  button: {
    marginTop: "20px",
    position: "relative",
  },
  dataGrid: {
    backgroundColor: "white",
  },
});

class SearchBar extends Component {
  constructor(props) {
    super(props);

    this.state = {
      searchQuery: "",
      queryResults: undefined,
      loading: false,
      errors: {},
    };
  }

  handleChange = (event) => {
    this.setState({
      [event.target.name]: event.target.value,
    });
  };

  handleSubmit = (event) => {
    event.preventDefault();
    let tokens = this.state.searchQuery.split(", ");
    var userData = "{";

    for (let i = 0; i < tokens.length; i++) {
      let split = tokens[i].split(":");
      userData += `"${split[0]}":"${split[1]}",\n`;
    }

    userData = userData.substring(0, userData.length - 2);
    userData += "\n}";

    let userDataJson = JSON.parse(userData);

    axios
      .post("/search", userDataJson, axiosConfig)
      .then((res) => {
        const results = res.data.relevantData;
        console.log(results);
        this.setState({
          queryResults: results,
          searchQuery: "",
        });
      })
      .catch((err) => console.log(err));
  };

  render() {
    const { classes } = this.props;

    return (
      <Grid container justify="center" alignItems="center" spacing={4}>
        <Grid item xs={8}>
          <form onSubmit={this.handleSubmit}>
            <TextField
              id="searchQuery"
              name="searchQuery"
              type="searchQuery"
              label="Search Elastic"
              placeholder="text:computer science, url:ucr, title:Riverside"
              value={this.state.searchQuery}
              onChange={this.handleChange}
              fullWidth
              className={classes.textField}
              variant="filled"
            />
            <Button type="submit" variant="contained" color="primary">
              SEARCH
            </Button>
          </form>
        </Grid>
        {this.state.queryResults && (
          <Grid item xs={10} className={classes.dataGrid}>
            <DataDisplay
              data={this.state.queryResults}
              dataGridClass={classes.dataGrid}
            />
          </Grid>
        )}
      </Grid>
    );
  }
}

export default withStyles(useStyles)(SearchBar);
