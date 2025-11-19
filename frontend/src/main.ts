// main.ts
import 'zone.js';
import { bootstrapApplication } from '@angular/platform-browser';
import { App } from './app/app';


// 1. Importe o appConfig
import { appConfig } from './app/app.config';

// 2. Passe o appConfig para o bootstrapApplication
bootstrapApplication(App, appConfig)
  .catch(err => console.error(err));