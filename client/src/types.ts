export interface User {
  email: string;
  name?: string | null;
  surname?: string | null;
}

export interface VKGroup {
  name: string;
  photo_url: string | null;
}

export interface VKPost {
  likes: number;
  reposts: number;
  views: number;
  timestamp: number;
  is_pinned: boolean;
  text: string;
  photos_url: string[] | null;
}

export interface PostponedItem {
  id: string;
  text: string | null;
  media_path: string | null;
  group_domain: string;
  created_at: string;
  scheduled: string;
}
