import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms'; 
import { Router, RouterLink } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';

// Angular Material
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    FormsModule, MatCardModule, MatInputModule,
    MatFormFieldModule, MatButtonModule,
    RouterLink, HttpClientModule
  ],
  templateUrl: './login.html',
  styleUrls: ['login.css']
})
export class Login {
  email = '';
  password = '';

  constructor(private http: HttpClient, private router: Router) {}

  onLogin() {
    if (!this.email || !this.password) {
      alert('Preencha todos os campos');
      return;
    }

    this.http.post('http://127.0.0.1:5000/api/login', { email: this.email, password: this.password })
      .subscribe({
        next: (res: any) => {
          localStorage.setItem('access_token', res.access_token);
          this.router.navigate(['/inicio']);
        },
        error: (err) => alert(err.error?.message || 'Email ou senha inválidos')
      });
  }
}
