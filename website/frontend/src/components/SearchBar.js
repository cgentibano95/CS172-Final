import React, { Component } from "react";
import axios from "axios";

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
});

class SearchBar extends Component {
  constructor(props) {
    super(props);

    this.state = {
      searchQuery: "",
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
      .then((res) => console.log(res))
      .catch((err) => console.log(err));
  };

  render() {
    const { classes } = this.props;
    return (
      <Grid container justify="center" alignItems="center">
        <Grid item>
          <form onSubmit={this.handleSubmit}>
            <TextField
              id="searchQuery"
              name="searchQuery"
              type="searchQuery"
              label="Search Elastic"
              placeholder="text:computer science, url:ucr, title:Riverside"
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
      </Grid>
    );
  }
}

export default withStyles(useStyles)(SearchBar);
