-- EstateX Phase 1 relational schema (PostgreSQL)

CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  phone VARCHAR(20) UNIQUE NOT NULL,
  role VARCHAR(20) NOT NULL CHECK (role IN ('buyer','seller','broker','admin')),
  kyc_status VARCHAR(20) NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE brokers (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  agency_name VARCHAR(255) NOT NULL,
  license_doc_url TEXT NOT NULL,
  rating NUMERIC(3,2) DEFAULT 0.00
);

CREATE TABLE properties (
  id BIGSERIAL PRIMARY KEY,
  broker_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  address TEXT NOT NULL,
  city VARCHAR(120) NOT NULL,
  price NUMERIC(14,2) NOT NULL,
  bhk SMALLINT NOT NULL,
  description TEXT NOT NULL,
  amenities JSONB DEFAULT '[]'::jsonb,
  verification_status VARCHAR(20) DEFAULT 'pending',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE verification_records (
  id BIGSERIAL PRIMARY KEY,
  property_id BIGINT REFERENCES properties(id) ON DELETE CASCADE,
  geo_lat NUMERIC(9,6) NOT NULL,
  geo_lng NUMERIC(9,6) NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
  face_match_score NUMERIC(5,2) NOT NULL,
  result VARCHAR(50) NOT NULL
);

CREATE TABLE cobroker_requests (
  id BIGSERIAL PRIMARY KEY,
  listing_id BIGINT REFERENCES properties(id) ON DELETE CASCADE,
  requester_broker_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
  listing_broker_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
  split_percentage NUMERIC(5,2) NOT NULL,
  status VARCHAR(20) DEFAULT 'pending'
);

CREATE TABLE negotiation_history (
  id BIGSERIAL PRIMARY KEY,
  listing_id BIGINT REFERENCES properties(id) ON DELETE CASCADE,
  from_user BIGINT REFERENCES users(id) ON DELETE CASCADE,
  to_user BIGINT REFERENCES users(id) ON DELETE CASCADE,
  amount NUMERIC(14,2) NOT NULL,
  message TEXT,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE transactions (
  id BIGSERIAL PRIMARY KEY,
  buyer_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
  seller_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
  listing_id BIGINT REFERENCES properties(id) ON DELETE CASCADE,
  amount NUMERIC(14,2) NOT NULL,
  status VARCHAR(20) NOT NULL,
  provider_reference VARCHAR(255)
);

CREATE TABLE video_tours (
  id BIGSERIAL PRIMARY KEY,
  listing_id BIGINT REFERENCES properties(id) ON DELETE CASCADE,
  host_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
  scheduled_at TIMESTAMP WITH TIME ZONE NOT NULL,
  recording_url TEXT
);
