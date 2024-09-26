# my-dash-app

This repo is made as an example of an error I keep getting when trying to update a table with a large dataset.

I'm trying to use a callback to store data into a dcc.Store component and then have another callback that is triggered by the modified_timestamp property of the store.

The error is as follows:

*Maximum update depth exceeded. This can happen when a component repeatedly calls setState inside componentWillUpdate or componentDidUpdate. React limits the number of nested updates to prevent infinite loops.*

It appears that the size of the dataset is a factor in causing the error but I'm uncertain.