import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from "@angular/common/http";
import {Observable} from "rxjs";
import {Podcast} from "./podcast";
import {API_URL} from "./env";
import {catchError} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class PodcastsApiService {

  constructor(private http: HttpClient) {
  }

  private static _handleError(err: HttpErrorResponse | any) {
    console.log(err);
    return Observable.throw(err.message || 'Error: Unable to complete request.');
  }

  getPodcasts(): Observable<Podcast[]> {
    return this.http
      .get<Podcast[]>(`${API_URL}/podcasts`)
      .pipe(catchError(PodcastsApiService._handleError));
  }

}
