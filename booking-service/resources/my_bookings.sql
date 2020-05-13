SELECT Bookings.booking_id, Bookings.start_date, Bookings.end_date, Accomodations.Name
FROM Bookings
         INNER JOIN Accomodations ON Bookings.accomodation_id = Accomodations.accomodation_id
WHERE Bookings.user_id = {userid};