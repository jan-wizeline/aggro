  -- Selecting companies that's hiring for React Developers
SELECT
  employer,
  position,
  location,
  urgency,
  details
FROM
  `experiments.202005_glassdoor1`
WHERE
  urgency IS NOT NULL
  AND employerRating > 2.0 AND 
  LOWER(description) LIKE '%react%' OR
  EXISTS (
    SELECT
      *
    FROM
      UNNEST(details) AS d
    WHERE
      LOWER(d) LIKE '%react%'
  )
  
-- Selecting companies that's hiring for java|react|node|gcp|amazon Developers
SELECT
  employer,
  position,
  location,
  urgency,
  details
FROM
  `experiments.202005_glassdoor1`
WHERE
  urgency IS NOT NULL
  AND employerRating > 2.0 AND 
  REGEXP_CONTAINS(LOWER(description), '/(java|react|node|gcp|amazon)/')
  OR
  EXISTS (
    SELECT
      *
    FROM
      UNNEST(details) AS details
    WHERE
      REGEXP_CONTAINS(LOWER(details), '/(java|react|node|gcp|amazon)/')
  )

----
-- Select frontend developers
SELECT
  employer,
  position,
  location,
  urgency,
FROM
  `aggro-dev-5609fefd.experiments.202005_glassdoor1`
WHERE
  EXISTS (
  SELECT
    *
  FROM
    UNNEST(details) AS details
  WHERE
    (LOWER(details) LIKE '%javascript%'
      OR LOWER(details) LIKE '%react%'
      OR LOWER(details) LIKE '%js%'
      OR LOWER(details) LIKE '%typescript%'
      OR LOWER(description) LIKE '%node%'
      OR LOWER(details) LIKE '%frontend%') )

---
-- List down the companies in one location that is in high demand of frontend engineers 
SELECT
  employer,
  location,
  COUNT(employer) AS count
FROM
  `experiments.202005_glassdoor1_frontend`
GROUP BY
  employer,
  location
ORDER BY
  count DESC

