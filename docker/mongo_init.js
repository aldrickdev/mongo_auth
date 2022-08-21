// Creates a users collection
db.createCollection("User")

// Creates a admin user in the greymint application
db.User.insertOne({
    username: "greymint_admin",
    email: "admin@greymint.com",
    hashed_password: "pass",
    role: "admin",
})