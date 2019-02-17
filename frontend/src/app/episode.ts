import {Podcast} from "./podcast";

export class Episode {
  id: number;
  podcast: Podcast;
  title: string;
  publication_timestamp: Date;
  audio_url: string;
  image_url: string;
  description: string;
  duration: number;
  episode_number: number;
  episode_part: number;
  status: string;
  needs_review: boolean;
}
