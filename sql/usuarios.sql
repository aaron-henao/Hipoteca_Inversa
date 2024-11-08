-- Drop tables if they already exist (for resetting purposes)
DROP TABLE IF EXISTS Mortgage;
DROP TABLE IF EXISTS Usuarios;

-- Create Usuarios table
CREATE TABLE IF NOT EXISTS Usuarios (
    cedula INT PRIMARY KEY,              -- Unique identifier for each user
    edad VARCHAR(2) NOT NULL,             -- User's age
    estado_civil TEXT NOT NULL,           -- Marital status
    edad_conyuge VARCHAR(2),             -- Spouse's age (optional)
    sexo_conyuge TEXT,                   -- Spouse's gender (optional)
    valor_inmueble VARCHAR(20) NOT NULL,  -- Value of the property
    condicion_inmueble TEXT NOT NULL,     -- Property condition (e.g., "good", "excellent")
    tasa_interes VARCHAR(4) NOT NULL      -- Interest rate as a string (e.g., "0.05" for 5%)
);

-- Create Mortgage table with a foreign key relationship to Usuarios
CREATE TABLE IF NOT EXISTS Mortgage (
    id SERIAL PRIMARY KEY,                    -- Unique identifier for each mortgage record
    user_id INT REFERENCES Usuarios(cedula) ON DELETE CASCADE,  -- References user in Usuarios
    total_payment FLOAT NOT NULL              -- Total mortgage payment amount
);


