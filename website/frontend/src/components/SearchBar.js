import React, { Component } from "react";

import withStyles from "@material-ui/core/styles/withStyles";
import Grid from "@material-ui/core/Grid";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";

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
      sort: "recent",
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
    const userQuery = { ...this.state.searchQuery.split(", ") };
    console.log(userQuery);
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
