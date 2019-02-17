import { TestBed } from '@angular/core/testing';

import { PodcastsApiService } from './podcasts-api.service';

describe('PodcastsApiService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: PodcastsApiService = TestBed.get(PodcastsApiService);
    expect(service).toBeTruthy();
  });
});
