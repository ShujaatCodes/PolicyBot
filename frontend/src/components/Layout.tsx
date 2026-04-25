import { Link, useNavigate } from 'react-router-dom';
import { LogOut, MessageSquare, Settings } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export function Layout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-6">
            <span className="text-lg font-bold text-[#29ABE2]">PolicyBot</span>
            <Link
              to="/chat"
              className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-[#29ABE2] transition-colors"
            >
              <MessageSquare size={15} />
              Chat
            </Link>
            {user?.role === 'admin' && (
              <Link
                to="/admin"
                className="flex items-center gap-1.5 text-sm text-gray-600 hover:text-[#29ABE2] transition-colors"
              >
                <Settings size={15} />
                Admin
              </Link>
            )}
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-400">{user?.email}</span>
            <button
              onClick={handleLogout}
              className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-red-500 transition-colors"
            >
              <LogOut size={15} />
              Logout
            </button>
          </div>
        </div>
      </nav>
      <main>{children}</main>
    </div>
  );
}
