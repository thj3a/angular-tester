import { ComponentFixture, TestBed } from '@angular/core/testing';
import { UserCardComponent, User } from './sample.component';

describe('UserCardComponent', () => {
  let component: UserCardComponent;
  let fixture: ComponentFixture<UserCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserCardComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UserCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('Input handling', () => {
    it('should accept a user object as input', () => {
      const testUser: User = {
        id: 1,
        name: 'John Doe',
        email: 'john@example.com'
      };

      component.user = testUser;
      expect(component.user).toEqual(testUser);
    });

    it('should handle null user input', () => {
      component.user = null;
      expect(component.user).toBeNull();
    });
  });

  describe('Output handling', () => {
    it('should emit edit event when onEdit is called with a valid user', () => {
      const testUser: User = {
        id: 1,
        name: 'John Doe',
        email: 'john@example.com'
      };

      component.user = testUser;
      spyOn(component.edit, 'emit');

      component.onEdit();

      expect(component.edit.emit).toHaveBeenCalledWith(testUser);
    });
  });
});