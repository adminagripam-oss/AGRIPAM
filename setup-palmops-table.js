const { supabase } = require('./api/lib/supabase'); // Using the correct path for supabase config: api/lib/supabase.js

const sql = `
CREATE TABLE IF NOT EXISTS database_palmops (
  id          BIGSERIAL PRIMARY KEY,
  tanggal     DATE NOT NULL,
  region      VARCHAR(100) NOT NULL,
  tonase      NUMERIC(10,2) NOT NULL DEFAULT 0,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  CONSTRAINT unique_palmops_tanggal_region UNIQUE (tanggal, region)
);

ALTER TABLE database_palmops ENABLE ROW LEVEL SECURITY;

-- Recreate policy to avoid duplicate error
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'database_palmops' AND policyname = 'block_public'
    ) THEN
        CREATE POLICY "block_public" ON database_palmops FOR ALL USING (false);
    END IF;
END
$$;

CREATE INDEX IF NOT EXISTS idx_palmops_tanggal ON database_palmops(tanggal);
CREATE INDEX IF NOT EXISTS idx_palmops_region ON database_palmops(region);
`;

async function setup() {
  console.log("Running database setup for database_palmops...");
  const { data, error } = await supabase.rpc('query', { 
    query_text: sql 
  });
  if (error) {
    console.error("Error creating table:", error);
  } else {
    console.log("database_palmops table and configurations successfully set up!");
  }
}

setup();
