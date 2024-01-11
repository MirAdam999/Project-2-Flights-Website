-- Creation of stored procedures for FlightsProject
use FlightsProject

--	get_airline_by_username(_username text)
GO
CREATE PROCEDURE get_airline_by_username
@username varchar
AS
	select * from AirlineCompanies ac
	inner join Users u 
	on u.UserID = ac.UserID
	where u.Username = @username
	
-- get_customer_by_username(_username text)
GO
CREATE PROCEDURE get_customer_by_username
@username varchar
AS
	select * from Customers c
	inner join Users u 
	on u.UserID = c.UserID
	where u.Username = @username

--get_user_by_username(_username tex)
GO
CREATE PROCEDURE get_user_by_username
@username varchar
AS
	select * from Users u
	where u.Username = @username

--get_flights_by_parameters(_origin_country_id int, _destination_country_id int,_date date)
GO
CREATE PROCEDURE get_flights_by_parameters
@origin_country_id int,
@destination_country_id int,
@date date
AS
	select * from Flights f
	where f.OriginCountryID=@origin_country_id 
	AND f.DestinationCountryID=@destination_country_id 
	AND CONVERT(DATE, f.DepartureTime)=@date

--get_flights_by_airline_ID(_airline_id bigint)
GO
ALTER PROCEDURE get_flights_by_airline_ID
@airlineID bigint
AS
	select * from Flights f
	where AirlineID = @airlineID

--get_arrival_flights_12hours(_country_id int)
GO
ALTER PROCEDURE get_arrival_flights_12hours
@countryID int
AS
	DECLARE @current_time DATETIME = GETDATE()
	select * from Flights f 
	where f.LandingTime >= @current_time
      AND f.LandingTime <= DATEADD(HOUR, 12, @current_time)
	  AND f.DestinationCountryID = @countryID

--get_departure_flights_12hours(_country_id int)
GO
CREATE PROCEDURE get_departure_flights_12hours
@countryID int
AS
	DECLARE @current_time DATETIME = GETDATE()
	select * from Flights f 
	where f.DepartureTime >= @current_time
      AND f.DepartureTime <= DATEADD(HOUR, 12, @current_time)
	  AND f.DestinationCountryID = @countryID

--get_tickets_by_customer(_customer_id int)
GO
CREATE PROCEDURE get_tickets_by_customer
@customerID int
AS
	select * from Tickets t
	where t.CustomerID = @customerID
