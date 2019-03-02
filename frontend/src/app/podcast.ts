import {Episode} from "./episode";

export class Podcast {
  id: number;
  title: string;
  image_url: URL;
  episodes: Episode[];
  summary: string;
}
