import {Component, OnInit} from '@angular/core';
import {Podcast} from "../podcast";
import {PodcastsApiService} from "../podcasts-api.service";

@Component({
  selector: 'app-podcasts',
  templateUrl: './podcasts.component.html',
  styleUrls: ['./podcasts.component.css']
})
export class PodcastsComponent implements OnInit {
  podcasts: Podcast[];

  constructor(private podcastsService: PodcastsApiService) {
  }

  ngOnInit() {
    this.getPodcasts();
  }

  getPodcasts(): void {
    this.podcastsService.getPodcasts()
      .subscribe(podcasts => this.podcasts = podcasts);
  }

}
