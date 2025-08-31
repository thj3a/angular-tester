import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { UserCardComponent } from './components/user-card.component';
import { User } from './components/user-card.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, UserCardComponent],
  template: `
    <h1>Welcome to {{ title() }}!</h1>
    
    <app-user-card [user]="user" (edit)="onUserEdit($event)"></app-user-card>

    <router-outlet />
  `,
  styles: [],
})
export class App {
  protected readonly title = signal('example-angular-app');
  
  user: User = {
    id: 1,
    name: 'John Doe',
    email: 'john.doe@example.com'
  };
  
  onUserEdit(user: User): void {
    console.log('User edited:', user);
  }
}