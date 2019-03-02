import {Episode} from "./episode";

export class Podcast {
  id: number;
  title: string;
  image_url: URL;
  episodes: Episode[];
  summary: string;
  statistics: PodcastStatistics;
}

export class PodcastStatistics {
  progress: string;
  num_in_progress: number;
  num_skipped: number;
  num_ignored: number;
  num_episodes: number;
  time_listened: number;
}
