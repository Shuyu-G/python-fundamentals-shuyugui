db = db.getSiblingDB("appdb");
db.createUser({
  user: "appuser",
  pwd: "apppass",
  roles: [{ role: "readWrite", db: "appdb" }],
});

db.users.drop();
db.users.insertMany([
  {
    username: "alice",
    email: "alice@example.com",
    profile: { full_name: "Alice Wang", age: 25, city: "Berlin" },
    tags: ["a", "x"],
    active: true,
  },
  {
    username: "bob",
    email: "bob@example.com",
    profile: { full_name: "Bob Lee", age: 30, city: "Bremen" },
    tags: ["b"],
    active: false,
  },
]);
