WITH raw AS (
  SELECT
    page,
    ROW_NUMBER() over() AS rn
  FROM
    all_sales
),
raw2 AS (
  SELECT
    page,
    rn,
    (
      rn -1
    ) AS p0,
    (
      rn -1
    ) // 1000 AS p1,
    (
      rn -1
    ) // 1000 + 1 AS p2
  FROM
    raw
)
SELECT
  *
FROM
  raw2
WHERE
  p2 <> page
