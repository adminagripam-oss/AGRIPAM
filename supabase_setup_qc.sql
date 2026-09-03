-- Script to create the QC Spreadsheet table

CREATE TABLE IF NOT EXISTS public.qc_spreadsheet (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    data JSONB NOT NULL DEFAULT '[]'::jsonb,
    columns JSONB NOT NULL DEFAULT '[]'::jsonb,
    settings JSONB NOT NULL DEFAULT '{}'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert a default row if empty so the API always has something to update
INSERT INTO public.qc_spreadsheet (id, data, columns, settings)
SELECT 
    '00000000-0000-0000-0000-000000000000'::uuid, 
    '[]'::jsonb, 
    '[{"id": "col1", "name": "Column 1", "type": "text"}]'::jsonb, 
    '{"fontFamily": "Inter, sans-serif", "fontSize": "14px"}'::jsonb
WHERE NOT EXISTS (
    SELECT 1 FROM public.qc_spreadsheet WHERE id = '00000000-0000-0000-0000-000000000000'
);
