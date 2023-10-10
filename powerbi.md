# GTMart PowerBI

## Organization

Inside the dash folder, we have 2 PowerBI files:

1) GTMartData.pbix - contains the specific connections for the data: sales and fuel
2) Fligh-Level-Sales-Dashboard-001.pbix (Dashboard) - the dashboard itself


The Dashboard connects with GTMartData, both need to de deployed in the PowerBI Services.


## Data Connection

The GTMartData connects to the database through an API Gateway. Below are the links:

1) Link to Sales: 
   - https://pbi-dt-bdg-277fd582e765.herokuapp.com/all_sales?apikey=\<APIKEY>

2) Link to Fuel:
   - https://pbi-dt-bdg-277fd582e765.herokuapp.com/all_fuel?apikey=\<APIKEY>


Both depend on the APIKEY, that will be provided in a separate email.

If you want to test the API Gateway, use the link:

`https://pbi-dt-bdg-277fd582e765.herokuapp.com/docs`


