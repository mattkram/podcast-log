import {Component, OnInit} from '@angular/core';
import {Podcast} from "../podcast";
import {PodcastService} from "../podcast.service";

@Component({
  selector: 'app-podcasts',
  templateUrl: './podcasts.component.html',
  styleUrls: ['./podcasts.component.css']
})
export class PodcastsComponent implements OnInit {
  podcasts$: Podcast[];

  constructor(private service: PodcastService) {
  }

  ngOnInit() {
    this.getPodcasts();
  }

  getPodcasts(): void {
    this.service.getPodcasts()
      .subscribe(podcasts => this.podcasts$ = podcasts);
  }

}
