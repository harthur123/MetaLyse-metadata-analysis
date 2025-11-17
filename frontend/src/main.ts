// main.ts
import 'zone.js';
import { bootstrapApplication } from '@angular/platform-browser';
import { App } from './app/app';
import { appConfig } from './app/app.config';

// 1. Importe o appConfig


// 2. Passe o appConfig para o bootstrapApplication
bootstrapApplication(App, appConfig)
  .catch(err => console.error(err));