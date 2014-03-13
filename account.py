import database

def get_information(user):
  query = database.UserData.gql("WHERE userid=:id", id=user.user_id())
  data = query.get()
  return data

def get_information_by_name(name):
  query = database.UserData.gql("WHERE name=:name", name=name)
  data = query.get()
  return data

def new_user(user, name, iidxid):
  database.UserData(
    userid = user.user_id(),
    name = name,
    iidxid = iidxid
    ).put()