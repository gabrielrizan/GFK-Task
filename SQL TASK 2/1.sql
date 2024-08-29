SELECT
    p.First_Name,
    p.Last_Name,
    p.Locatie,
    v.quality,
    COUNT(v.ID) AS votes_received
FROM
    persons p
LEFT JOIN
    Votes v ON p.ID = v.chosen_person
WHERE
    v.valid = 1
GROUP BY
    p.First_Name,
    p.Last_Name,
    p.Locatie,
    v.quality
ORDER BY
    p.Locatie,
    p.Last_Name,
    p.First_Name;
