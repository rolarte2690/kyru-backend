import sqlite3

def create_kyru_database(db_name="kyru_catalog.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Enable foreign key constraints in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Vehicles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        make TEXT NOT NULL,
        model TEXT NOT NULL,
        submodel_trim TEXT,
        engine TEXT,
        vin_pattern TEXT
    );
    """)

    # 2. Master Parts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS master_parts (
        master_part_id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_number_oem TEXT,
        part_name TEXT NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT NOT NULL,
        brand_manufacturer TEXT NOT NULL,
        weight_lbs REAL DEFAULT 0.0
    );
    """)

    # 3. Part Fitments Table (Junction Table)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS part_fitments (
        fitment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        master_part_id INTEGER NOT NULL,
        vehicle_id INTEGER NOT NULL,
        position TEXT,
        FOREIGN KEY (master_part_id) REFERENCES master_parts (master_part_id) ON DELETE CASCADE,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles (vehicle_id) ON DELETE CASCADE
    );
    """)

    # 4. Warehouses Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warehouses (
        warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier_name TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        state TEXT NOT NULL
    );
    """)

    # 5. Supplier Listings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS supplier_listings (
        listing_id INTEGER PRIMARY KEY AUTOINCREMENT,
        master_part_id INTEGER NOT NULL,
        warehouse_id INTEGER NOT NULL,
        supplier_sku TEXT NOT NULL,
        price_usd REAL NOT NULL,
        stock_quantity INTEGER DEFAULT 0,
        is_dropship INTEGER DEFAULT 0, -- 0 for False, 1 for True
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (master_part_id) REFERENCES master_parts (master_part_id) ON DELETE CASCADE,
        FOREIGN KEY (warehouse_id) REFERENCES warehouses (warehouse_id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print(f"Database successfully created/verified: {db_name}")

if __name__ == "__main__":
    create_kyru_database()