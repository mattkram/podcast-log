import {Component, OnInit} from '@angular/core';
import {Episode} from "../episode";
import {EpisodeService} from "../episode.service";

@Component({
  selector: 'app-episodes',
  templateUrl: './episodes.component.html',
  styleUrls: ['./episodes.component.css']
})
export class EpisodesComponent implements OnInit {
  episodes: Episode[];

  constructor(private episodeService: EpisodeService) {
  }

  ngOnInit() {
    this.getEpisodes();
  }

  getEpisodes(): void {
    this.episodeService.getAllEpisodes()
      .subscribe(episodes => this.episodes = episodes);
  }

}
