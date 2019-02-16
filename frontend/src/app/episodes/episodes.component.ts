import {Component, OnInit} from '@angular/core';
import {Episode} from "../episode";
import {EPISODES} from "../mock-episodes";

@Component({
  selector: 'app-episodes',
  templateUrl: './episodes.component.html',
  styleUrls: ['./episodes.component.css']
})
export class EpisodesComponent implements OnInit {
  episodes: Episode[];

  constructor() {
  }

  ngOnInit() {
    this.getEpisodes();
  }

  getEpisodes(): void {
    this.episodes = EPISODES
  }

}
