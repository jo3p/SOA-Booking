SELECT accomodation_id, SUM(price) as total_price
FROM Pricing
WHERE accomodation_id IN {accomodations_string} AND date BETWEEN '{start_date}' AND '{end_date}'
GROUP BY accomodation_id;