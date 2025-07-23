import React, { useEffect, useState, useContext } from 'react';
import { Modal, Input, Card, Typography, Button, Spin, message } from 'antd';
import { ProjectContext } from '../context/ProjectContext';
import { useAuth } from '../context/AuthContext';

const { Title, Paragraph } = Typography;

export default function ProjectSearchModal({ visible, onClose }) {
  const { selectedProject, projectMembers, currentUser } = useContext(ProjectContext);
  const { isAdmin } = useAuth();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [requesting, setRequesting] = useState({}); // { [projectId]: boolean }
  const [requested, setRequested] = useState({}); // { [projectId]: true }
  const [memberOf, setMemberOf] = useState({}); // { [projectId]: true }
  const [userProjects, setUserProjects] = useState([]);

  useEffect(() => {
    if (visible && currentUser) {
      fetchProjects();
      fetchUserProjects();
    }
  }, [visible, currentUser]);

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const res = await import('../utils/api').then(m => m.apiFetch('/all-projects'));
      if (res.ok) {
        const data = await res.json();
        setProjects(data.projects || []);
      }
    } catch {}
    setLoading(false);
  };

  const fetchUserProjects = async () => {
    try {
      const res = await import('../utils/api').then(m => m.apiFetch(`/users/${currentUser.id}`));
      if (res.ok) {
        const data = await res.json();
        setUserProjects(data.user.projects || []);
      }
    } catch {}
  };

  const handleRequest = async (projectId) => {
    setRequesting(r => ({ ...r, [projectId]: true }));
    try {
      const res = await import('../utils/api').then(m => m.apiFetch(`/projects/${projectId}/join-request`, { method: 'POST' }));
      const data = await res.json();
      if (res.ok) {
        setRequested(r => ({ ...r, [projectId]: true }));
        message.success('Join request sent!');
      } else {
        message.error(data.error || 'Failed to send join request');
      }
    } catch {
      message.error('Network error');
    }
    setRequesting(r => ({ ...r, [projectId]: false }));
  };

  // Optionally, you could fetch user's pending requests and memberships to set requested/memberOf

  let filtered = projects.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    (p.description && p.description.toLowerCase().includes(search.toLowerCase()))
  );

  // If not admin, only show projects the user is not already a member of as owner or contributor
  if (!isAdmin && currentUser) {
    filtered = filtered.filter(project =>
      !userProjects.some(p =>
        p.id === project.id &&
        (p.role === 'Project Owner' || p.role === 'Project Contributor')
      )
    );
  }

  return (
    <Modal
      title="Search Projects"
      open={visible}
      onCancel={onClose}
      footer={null}
      width={700}
    >
      <Input.Search
        placeholder="Search projects..."
        value={search}
        onChange={e => setSearch(e.target.value)}
        style={{ marginBottom: 24 }}
      />
      {loading ? <Spin /> : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '24px' }}>
          {filtered.map(project => {
            const isMember = projectMembers.some(m => m.project_id === project.id && m.user_id === currentUser?.id);
            return (
              <Card key={project.id} title={project.name}>
                <Paragraph type="secondary">{project.description || 'No description'}</Paragraph>
                {isAdmin ? (
                  <Button
                    type="primary"
                    onClick={() => window.location.href = `/projects/${project.id}`}
                    style={{ marginTop: 12 }}
                  >
                    Go to Project
                  </Button>
                ) : (
                  <Button
                    type="primary"
                    disabled={isMember || requested[project.id]}
                    loading={requesting[project.id]}
                    onClick={() => handleRequest(project.id)}
                    style={{ marginTop: 12 }}
                  >
                    {isMember ? 'Already a Member' : requested[project.id] ? 'Request Pending' : 'Request to Join'}
                  </Button>
                )}
              </Card>
            );
          })}
        </div>
      )}
    </Modal>
  );
} 