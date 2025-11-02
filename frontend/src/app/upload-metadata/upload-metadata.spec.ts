import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadMetadata } from './upload-metadata';

describe('UploadMetadata', () => {
  let component: UploadMetadata;
  let fixture: ComponentFixture<UploadMetadata>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UploadMetadata]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UploadMetadata);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
