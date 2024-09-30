import React, { useState } from 'react';

const MigrationForm = () => {
  const [mysql, setMySQL] = useState('');
  const [mongo, setMongo] = useState('');
  const [mysqlTable, setMySQLTable] = useState('');
  const [mongoCollection, setMongoCollection] = useState('');
  const [mongoDB, setMongoDB] = useState(''); // New state for MongoDB database name

  const handleSubmit = async (event) => {
    event.preventDefault();

    const response = await fetch('http://localhost:8000/api/migrate/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        mysql,
        mongo,
        mysql_table: mysqlTable,         // Include the table name
        mongo_collection: mongoCollection, // Include the collection name
        mongo_db: mongoDB                 // Include the MongoDB database name
      }),
    });

    const data = await response.json();
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>MySQL Connection String</label>
        <input type="text" value={mysql} onChange={(e) => setMySQL(e.target.value)} />
      </div>
      <div>
        <label>MongoDB Connection String</label>
        <input type="text" value={mongo} onChange={(e) => setMongo(e.target.value)} />
      </div>
      <div>
        <label>MySQL Table Name</label>
        <input type="text" value={mysqlTable} onChange={(e) => setMySQLTable(e.target.value)} />
      </div>
      <div>
        <label>MongoDB Collection Name</label>
        <input type="text" value={mongoCollection} onChange={(e) => setMongoCollection(e.target.value)} />
      </div>
      <div>
        <label>MongoDB Database Name</label>
        <input type="text" value={mongoDB} onChange={(e) => setMongoDB(e.target.value)} />
      </div>
      <button type="submit">Migrate</button>
    </form>
  );
};

export default MigrationForm;
