-- Creation of stored procedures for FlightsProject
use FlightsProject

--	get_airline_by_username(_username text)
GO
ALTER PROCEDURE get_airline_by_username
@username varchar(50)
AS
	select * from AirlineCompanies ac
	inner join Users u 
	on u.UserID = ac.UserID
	where u.Username = @username
	
-- get_customer_by_username(_username text)
GO
ALTER PROCEDURE get_customer_by_username
-- Author:		<Author,,Name>
-- Create date: <Create Date,,>
-- Description:	<Description,,>
@username varchar(50)
AS
	select * from Customers c
	inner join Users u 
	on u.UserID = c.UserID
	where u.Username = @username

--get_user_by_username(_username tex)
GO
ALTER PROCEDURE get_user_by_username
@username varchar(50)
AS
	select * from Users u
	where u.Username = @username

--get_flights_by_parameters(_origin_country_id int, _destination_country_id int,_date date)
GO
ALTER PROCEDURE get_flights_by_parameters
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
ALTER PROCEDURE get_departure_flights_12hours
@countryID int
AS
	DECLARE @current_time DATETIME = GETDATE()
	SELECT * FROM Flights f 
	WHERE f.DepartureTime >= @current_time
      AND f.DepartureTime <= DATEADD(HOUR, 12, @current_time)
	  AND f.OriginCountryID = @countryID

--get_tickets_by_customer(_customer_id int)
GO
CREATE PROCEDURE get_tickets_by_customer
@customerID int
AS
	select * from Tickets t
	where t.CustomerID = @customerID

--EXTRAS-insted of funcs

--getFlightsByOriginCountryId(country_id)
GO
CREATE PROCEDURE get_flights_by_origin_country_ID
@origin_countryID int
AS
	select * from Flights f
	where f.OriginCountryID = @origin_countryID

--getFlightsByDestinationCountryId(country_id)
GO
CREATE PROCEDURE get_flights_by_destination_country_ID
@destination_countryID int
AS
	select * from Flights f
	where f.DestinationCountryID = @destination_countryID

--getFlightsByDepartureDate(date)
GO
ALTER PROCEDURE get_flights_by_departure_date
@departure_date date
AS
	select * from Flights f
	where convert (date, f.DepartureTime) = @departure_date

--getFlightsByLandingDate(date)
GO
CREATE PROCEDURE get_flights_by_landing_date
@landing_date date
AS
	select * from Flights f
	where convert (date, f.LandingTime) = @landing_date

--getFlightsByCustomer(customer)???

--getAirlinesByCountry(country_id)
GO
CREATE PROCEDURE get_airlines_by_country
@countryID int
AS
	select * from AirlineCompanies ac
	where ac.Country_ID = @countryID

-- EXTRAS- buisness logic 
--FacadeBase
GO
CREATE PROCEDURE get_airline_by_userID
@userID bigint
AS
	select * from AirlineCompanies ac
	where ac.UserID = @userID


--Extras
GO
CREATE PROCEDURE get_admin_by_username
@username varchar(50)
AS
	select * from Administrators a
	inner join Users u 
	on u.UserID = a.UserID
	where u.Username = @username

GO
CREATE PROCEDURE check_if_customer_owns_ticket_for_flight
@flightID bigint,
@customerID bigint
AS
	select * from Tickets t
	where t.CustomerID = @customerID
	and t.FlightID = @flightID

GO
CREATE PROCEDURE get_customer_by_userID
@userID bigint
AS
	select * from Customers c
	where c.UserID = @userID

GO
CREATE PROCEDURE get_admin_by_userID
@userID bigint
AS
	select * from Administrators a
	where a.UserID = @userID

GO
ALTER PROCEDURE check_if_flight_exists
@origin_country_id int,
@destination_country_id int,
@datetime datetime
AS
	select * from Flights f
	where f.OriginCountryID=@origin_country_id 
	AND f.DestinationCountryID=@destination_country_id 
	AND f.DepartureTime=@datetime

GO
CREATE PROCEDURE buy_ticket
@flightID int
AS
	DECLARE @CurrentTickets INT;

    SELECT @CurrentTickets = f.RemainingTickets
    FROM Flights f
    WHERE f.FlightID = @FlightID;

    UPDATE Flights 
	SET RemainingTickets = @CurrentTickets - 1
    WHERE  Flights.FlightID= @FlightID;

GO
CREATE PROCEDURE return_ticket
@flightID int
AS
	DECLARE @CurrentTickets INT;

    SELECT @CurrentTickets = f.RemainingTickets
    FROM Flights f
    WHERE f.FlightID = @FlightID;

    UPDATE Flights 
	SET RemainingTickets = @CurrentTickets + 1
    WHERE  Flights.FlightID= @FlightID;

GO
CREATE PROCEDURE get_tickets_by_flightID
@flightID bigint
AS
	select * from Tickets t
	where t.FlightID = @flightID

GO
CREATE PROCEDURE check_if_airline_or_admin_exists
@username varchar (50),
@email varchar (50),
AS
	SELECT * FROM Users u
	WHERE u.Username = @username
	or u.Email = @email


