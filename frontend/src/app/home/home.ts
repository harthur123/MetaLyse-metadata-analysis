// ARQUIVO: src/app/home/home.ts

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { MatIconModule } from '@angular/material/icon'; 
import { MatCardModule } from '@angular/material/card'; 

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule,
    MatCardModule
  ],
  templateUrl: './home.html', // Nome do arquivo sem .component
  styleUrl: './home.css'      // Nome do arquivo sem .component
})
export class Home {
  // ...
}