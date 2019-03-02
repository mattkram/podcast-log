import {Component, OnInit} from '@angular/core';
import {PodcastService} from "../podcast.service";
import {Podcast} from "../podcast";
import {ActivatedRoute, ParamMap, Router} from "@angular/router";
import {switchMap} from "rxjs/operators";
import {Observable} from "rxjs";

@Component({
  selector: 'app-podcast-detail',
  templateUrl: './podcast-detail.component.html',
  styleUrls: ['./podcast-detail.component.css']
})
export class PodcastDetailComponent implements OnInit {

  podcast$: Observable<Podcast>;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private service: PodcastService) {
  }

  ngOnInit() {
    this.podcast$ = this.route.paramMap.pipe(
      switchMap((params: ParamMap) =>
        this.service.getPodcast(params.get('id')))
    );
  }

}
