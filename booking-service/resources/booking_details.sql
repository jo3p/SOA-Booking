SELECT Bookings.booking_id,
       Bookings.start_date,
       Bookings.end_date,
       Bookings.total_amount,
       Bookings.paid,
       Bookings.refunded,
       Accomodations.Name,
       Accomodations.City,
       Accomodations.Country
FROM Bookings
         INNER JOIN Accomodations ON Bookings.accomodation_id = Accomodations.accomodation_id
WHERE booking_id = '{bookingid}';