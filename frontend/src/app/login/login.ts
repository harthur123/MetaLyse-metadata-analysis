import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';

// Angular Material
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    FormsModule,
    CommonModule,
    HttpClientModule,
    RouterLink,
    MatCardModule,
    MatInputModule,
    MatFormFieldModule,
    MatButtonModule,
    MatCheckboxModule,
    MatIconModule,
    MatProgressSpinnerModule
  ],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {

  private http = inject(HttpClient);
  private router = inject(Router);

  email = localStorage.getItem('saved_email') || '';
  password = '';
  hidePassword = true;
  loading = false;
  errorMsg = '';
  remember = false;

  validateEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  onLogin() {
    this.errorMsg = '';

    if (!this.email || !this.password) {
      this.errorMsg = 'Preencha todos os campos.';
      return;
    }

    if (!this.validateEmail(this.email)) {
      this.errorMsg = 'E-mail inválido.';
      return;
    }

    const body = { email: this.email, password: this.password };
    this.loading = true;

    this.http.post('http://127.0.0.1:5000/api/auth/login', body)
      .subscribe({
        next: (res: any) => {
          this.loading = false;

          localStorage.setItem('access_token', res.access_token);

          if (this.remember) {
            localStorage.setItem('saved_email', this.email);
          } else {
            localStorage.removeItem('saved_email');
          }

          this.router.navigate(['/inicio']);
        },
        error: (err) => {
          this.loading = false;
          if (err.status === 401) this.errorMsg = 'Senha incorreta.';
          else if (err.status === 404) this.errorMsg = 'Usuário não encontrado.';
          else this.errorMsg = 'Erro ao conectar ao servidor.';
        }
      });
  }
}
