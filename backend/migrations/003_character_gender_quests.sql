ALTER TABLE character ADD COLUMN IF NOT EXISTS gender VARCHAR(16) NOT NULL DEFAULT 'UNSET';

CREATE TABLE IF NOT EXISTS quest (
  code VARCHAR(64) PRIMARY KEY,
  title VARCHAR(128) NOT NULL,
  summary VARCHAR(512) NOT NULL,
  objective VARCHAR(256) NOT NULL,
  required_progress INTEGER NOT NULL DEFAULT 1 CHECK (required_progress > 0),
  reward_xp INTEGER NOT NULL DEFAULT 0 CHECK (reward_xp >= 0),
  sort_order INTEGER NOT NULL DEFAULT 0,
  status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS character_quest (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  character_id UUID NOT NULL REFERENCES character(id),
  quest_code VARCHAR(64) NOT NULL REFERENCES quest(code),
  state VARCHAR(32) NOT NULL DEFAULT 'IN_PROGRESS',
  progress INTEGER NOT NULL DEFAULT 0 CHECK (progress >= 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (character_id, quest_code)
);

CREATE INDEX IF NOT EXISTS idx_character_quest_character ON character_quest(character_id);

INSERT INTO quest (code, title, summary, objective, required_progress, reward_xp, sort_order) VALUES
  ('ECHO_AWAKENING', 'Tiếng vọng đầu tiên', 'Ký ức của vùng đất đang rạn vỡ. Hãy chạm vào tinh thể ký ức để nghe tiếng vọng.', 'Chạm vào Memory Crystal', 1, 50, 1),
  ('FOREST_SURVEY', 'Khảo sát rừng Mộc Vọng', 'Người gác rừng cần biết chuyện gì đang xảy ra sau hàng cây.', 'Đi tới 3 mốc trong rừng', 3, 80, 2),
  ('WOLF_CULL', 'Bầy sói rêu', 'Sói rêu đã tràn xuống gần trại. Dẹp chúng trước khi có người bị thương.', 'Hạ 3 Moss Wolf', 3, 120, 3),
  ('SHRINE_OFFERING', 'Lễ vật cho đền Vọng', 'Đền Vọng im lặng đã lâu. Một lễ vật đúng cách có thể đánh thức nó.', 'Dâng lễ tại Echo Shrine', 1, 100, 4),
  ('MERCHANT_ERRAND', 'Chuyến hàng của thương nhân', 'Thương nhân ở chợ cần người đáng tin đưa hàng qua cầu gỗ.', 'Giao hàng tới Market Stall', 1, 70, 5)
ON CONFLICT (code) DO NOTHING;
