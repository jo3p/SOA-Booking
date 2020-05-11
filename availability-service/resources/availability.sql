SELECT accomodation_id
FROM Accomodations
WHERE city = '{city}' AND
      country = '{country}' AND
      accomodation_id IN (
          SELECT accomodation_id
          FROM Availability
          WHERE capacity >= '{n_persons}' AND date BETWEEN '{start_date}' AND '{end_date}'
          GROUP BY accomodation_id
          HAVING COUNT(accomodation_id) = '{length_stay}'
        );