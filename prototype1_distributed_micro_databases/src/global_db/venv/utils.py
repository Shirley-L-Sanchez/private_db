import sqlparse
def execute_query(q, c):
  assert(len(sqlparse.parse(q)) == 1)
  c.execute(q)
  fields = [field_meta[0] for field_meta in c.description]
  result = [dict(zip(fields,row)) for row in c.fetchall()]
  return result