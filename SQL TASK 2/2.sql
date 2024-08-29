SELECT
    p.Locatie AS country,
    COUNT(v.ID) AS votes_received
FROM
    persons p
LEFT JOIN
    Votes v ON p.ID = v.chosen_person AND v.valid = 1
GROUP BY
    p.Locatie
ORDER BY
    p.Locatie;
