// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';

// Use o caminho que você usou no main.ts
import { routes } from './app.routes'; 

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes), 
    provideHttpClient(withFetch()),
    provideAnimations() // Importante para o Angular Material
  ]
};